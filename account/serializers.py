from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Role, RolePerm, Perm


User = get_user_model()




class PermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perm
        fields = ['name', 'codename', 'perm_model', 'action', 'field', 'lang']

class RolePermSerializer(serializers.ModelSerializer):
    perm = PermSerializer()

    class Meta:
        model = RolePerm
        fields = ['perm', 'value']

class RoleSerializer(serializers.ModelSerializer):
    role_permset = RolePermSerializer(many=True)

    class Meta:
        model = Role
        fields = ['name', 'role_permset']






class FieldPermissionSerializer(serializers.ModelSerializer):
    """
    A base serializer that checks field-level permissions for both read and write operations.
    Other serializers can inherit this class to apply field-level access control.
    """

    def to_representation(self, instance):
        """
        Override to control the fields that are returned in the response based on user's field-level permissions.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request')
        user = request.user

        # Get the ContentType for the instance (model)
        content_type = ContentType.objects.get_for_model(instance)

        # Filter the fields that the user has permission to view
        allowed_fields = self.get_allowed_fields(user, content_type, action='view', instance=instance)

        # Return only the fields the user has permission to see
        return {field: value for field, value in representation.items() if field in allowed_fields}

    def validate(self, attrs):
        """
        Override to control which fields the user can modify during create/update.
        """
        request = self.context.get('request')
        user = request.user

        # Get the action from the view (e.g., 'create', 'update')
        action = self.context['view'].action

        # Get the ContentType for the model the serializer is working with
        content_type = ContentType.objects.get_for_model(self.Meta.model)

        # Extract the fields being modified from the incoming data
        fields_to_modify = attrs.keys()

        # Check if the user has permission to modify these fields
        allowed_fields = self.get_allowed_fields(user, content_type, action=action)

        # Raise an error if the user tries to modify a field they don't have permission for
        for field in fields_to_modify:
            if field not in allowed_fields:
                raise serializers.ValidationError({field: "You do not have permission to modify this field."})

        return attrs

    def get_allowed_fields(self, user, content_type, action, instance=None):
        """
        Return the fields the user is allowed to access (either view or modify) based on their permissions.
        """
        allowed_fields = set()

        # Map DRF actions to your permission actions
        action_mapping = {
            'view': 'retrieve',  # Map 'view' action to 'retrieve' permission
            'list': 'view',      # For listing, we can use 'view'
            'retrieve': 'retrieve',  # Keep 'retrieve' as is
            'create': 'create',
            'update': 'update',
            'partial_update': 'update',
            'destroy': 'delete'
        }

        # Get the corresponding permission action
        permission_action = action_mapping.get(action, action)

        # Get all role permissions of the user
        user_permissions = user.role_perms.all()

        # Iterate over user permissions and check if they match the content type and action
        for user_permission in user_permissions:
            perm = user_permission.perm

            # Check if the permission applies to the correct model (content type) and action
            if perm.perm_model == content_type and perm.action == permission_action:
                # If the permission is for a specific field, add that field to allowed_fields
                if perm.field:
                    allowed_fields.add(perm.field)
                else:
                    # If no field restriction, allow all fields (wildcard permission)
                    allowed_fields.update(self.fields.keys())

        return allowed_fields

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['mobile', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Add mobile number validation logic if necessary
        mobile = attrs.get('mobile')
        if len(mobile) != 10:
            raise serializers.ValidationError({"mobile": "Mobile number must be 10 digits."})
        if not mobile.isdigit():
            raise serializers.ValidationError({"mobile": "Mobile number must contain only digits."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create(
            username=validated_data['mobile'],
            mobile=validated_data['mobile'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        mobile = data.get('mobile')
        password = data.get('password')

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError({"mobile": "Mobile number not found."})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password."})

        data['user'] = user
        return data
