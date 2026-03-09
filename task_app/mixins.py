class UserIsOwner:
    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user)
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    



