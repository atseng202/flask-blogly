# Utility methods for form validation
from flask import flash

def is_form_invalid(form_data, form_input_labels):
    """Checks the new user or edit user form data and
    makes sure that first_name and last_name are not empty.
    If there are invalid inputs, adds flash error messages
    and returns T/F.
    """

    invalid_ind = False

    for (key, label) in form_input_labels:
        if not form_data[key]:
            flash(f"{label} cannot be empty!")
            invalid_ind = True

    return invalid_ind