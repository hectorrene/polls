from django import forms 
from polls.models import Question, Choice

class new_questionForm (forms.Form):
    question = forms.CharField()
    choice = forms.CharField(widget=forms.Textarea)

    def save_question (self) :
        # Get the question text from the form
        question_text = self.cleaned_data['txtmpregunta']

        # Create a new Question object
        new_question = Question.objects.create(question_text=question_text)

        # Get the choices text from the form and split them into a list
        choices_text = self.cleaned_data['choices']
        choices_list = [choice.strip() for choice in choices_text.split('\n') if choice.strip()]

        # Create Choice objects and associate them with the new question
        for choice_text in choices_list:
            Choice.objects.create(question=new_question, choice_text=choice_text)

class updateQuestionForm (forms.ModelForm):
    class Meta: 
        Model : Question
        fields = ('pub_date', 'question_text')