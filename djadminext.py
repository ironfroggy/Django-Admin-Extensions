from django.contrib import admin

def extend_admin(model, old_admin, new_admin):

    already_extended = old_admin.__dict__.get('_extended_admin', None)
    if already_extended is not None:
        return extend_admin(model, already_extended, new_admin)

    admin.site.unregister(model)
    try:
        class _ExtendingAdmin(old_admin, new_admin):
            pass

        # Combine inline lists
        _ExtendingAdmin.inlines = (
            getattr(old_admin, 'inlines', []) +
            getattr(new_admin, 'inlines', [])
        )

        old_admin._extended_admin = _ExtendingAdmin

    except:
        admin.site.register(model, old_admin)
        raise
    else:
        admin.site.register(model, _ExtendingAdmin)

    return _ExtendingAdmin

