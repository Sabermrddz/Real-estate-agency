from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("messaging", "0011_rename_messaging_c_created_0b4cd8_idx_contact_mes_created_684d0e_idx_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="reservation",
            old_name="updated_at",
            new_name="status_updated_at",
        ),
    ]

