from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from recommendations.choices import GENRES, TRIGGER_DICT, TRIGGERS

GENRE_PREFERENCES = (
    ("like", "Like"),
    ("dislike", "Dislike"),
    ("block", "Block"),
    ("neutral", "No Preference"),
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class GenreForm(forms.Form):
    def __init__(self, *args, **kwargs):
        initial_preferences = kwargs.pop("initial_preferences", {})
        super(GenreForm, self).__init__(*args, **kwargs)
        for genre in GENRES:
            genre_value = genre[0]
            genre_label = genre[1]
            self.fields[genre_value] = forms.ChoiceField(
                choices=GENRE_PREFERENCES,
                label=genre_label,
                widget=forms.RadioSelect,
                required=False,
                initial=initial_preferences.get(genre_value, "neutral"),
            )

    def clean(self):
        cleaned_data = super(GenreForm, self).clean()
        all_block = True
        all_dislike = True

        for genre_value, _ in GENRES:
            preference = cleaned_data.get(genre_value)

            if preference != "block":
                all_block = False

            if preference != "dislike":
                all_dislike = False

            if not all_block and not all_dislike:
                return cleaned_data

        if all_block or all_dislike:
            raise forms.ValidationError(
                "Not all genres can be set to 'Block' or 'Dislike'. Please choose a different preference for at least one genre."
            )


class CustomTriggerForm(forms.Form):
    """
    This form is used to collect user preferences for each trigger,
    """

    # TODO
