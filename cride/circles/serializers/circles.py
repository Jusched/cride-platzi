"""Circle serializers"""

# Django REST Framework
from rest_framework import serializers
from django.db.models import fields

# Local modules
from cride.circles.models import Circle



class CircleModelSerializer(serializers.ModelSerializer):
    """Circle model serializer"""
        
    members_limit= serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=500
    )
    is_limited= serializers.BooleanField(default=False)

    class Meta:
        """Meta class"""

        model= Circle
# Fields should be used when there is no sensitive data in the model that we wouldn't want to show.
        fields= "__all__"

# Fields that can only be changed by admins
        read_only_fields=(
            "is_public",
            "verified",
            "rides_offered",
            "rides_taken"
        )

    def validate(self, data):
        """Ensures both members_limit and is_limited are valid."""

        members_limit= data.get("members_limit", None)
        is_limited= data.get("is_limited", False)

        if not members_limit and is_limited:
            raise serializers.ValidationError('If circle is limited, a member limit must be provided.')
        elif members_limit and not is_limited:
            raise serializers.ValidationError('If circle is not limited, a member limit must not be provided.')
        return data