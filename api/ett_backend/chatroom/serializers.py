from rest_framework import serializers

from chatroom.models import ChatRoom
from trees.models import TreeDetail


class ChatRoomCreateSerializer(serializers.Serializer):
    chat_room_uuid = serializers.UUIDField(read_only=True)
    chat_room_name = serializers.CharField(write_only=True)
    tree_uuid = serializers.UUIDField(write_only=True)

    def validate(self, attrs):
        if "chat_room_name" not in attrs:
            raise serializers.ValidationError({"chat_room_name": "This field is required."})
        if "tree_uuid" not in attrs:
            raise serializers.ValidationError({"tree_uuid": "This field is required."})
        return attrs


class ChatRoomSerializer(serializers.ModelSerializer):
    tree_uuid = serializers.SerializerMethodField()

    def get_tree_uuid(self, obj):
        return str(obj.tree.tree_uuid) if obj.tree else None

    class Meta:
        model = ChatRoom
        fields = ["chat_room_uuid", "chat_room_name", "tree_uuid", "created_at", "updated_at"]


class ChatRoomUpdateSerializer(serializers.ModelSerializer):
    tree_uuid = serializers.UUIDField(write_only=True, required=False)

    def validate(self, attrs):
        if "chat_room_name" in attrs and attrs["chat_room_name"] == "":
            return serializers.ValidationError("chat_room_name must not empty")
        if "tree_uuid" in attrs and attrs["tree_uuid"] == "":
            return serializers.ValidationError("tree_uuid must not empty")
        return attrs

    def update(self, instance, validated_data):
        tree_uuid = validated_data.pop("tree_uuid", None)
        if tree_uuid:
            tree = TreeDetail.objects.filter(tree_uuid=tree_uuid).first()
            if not tree:
                raise serializers.ValidationError("tree not found")
            instance.tree = tree

        instance.chat_room_name = validated_data.get("chat_room_name", instance.chat_room_name)
        instance.save()
        return instance

    class Meta:
        model = ChatRoom
        fields = [
            "chat_room_name",
            "tree_uuid",
        ]
        extra_kwargs = {
            "chat_room_name": {"required": False},
        }
