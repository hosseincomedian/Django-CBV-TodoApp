from rest_framework import serializers
from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    todo_url = serializers.SerializerMethodField(read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = Todo
        fields = (
            "id",
            "user",
            "title",
            "complete",
            "todo_url",
            "created_time",
            "updated_time",
        )
        read_only_fields = ("id", "user")

    def get_todo_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)

        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("todo_url", None)
        else:
            rep.pop("content", None)
        return rep

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)
