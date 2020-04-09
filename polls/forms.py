from django import forms

class ReviewForm(forms.Form):
	text =  forms.CharField(max_length=1000,widget=forms.Textarea(attrs={"rows":5, "cols":20,'placeholder': 'Enter Text'}))
	model=forms.ChoiceField(choices=[('Naive Bayes', 'Naive Bayes'), ('Gradient Boosting', 'Gradient Boosting'),('SVC', 'SVC'),('Random Forest', 'Random Forest'),('KNN', 'KNN'),('RNN', 'RNN')])