from django import forms
from django.contrib.auth.models import User
from django.core import validators
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, Field
from .choices import STATE_CHOICES, PREPARO_ESCOLHAS
from .models import PerfilUsuario, Receita, Comentario, Categoria
from datetime import date


class CharacterUpperField(forms.CharField):
    def validate(self, value):
        if not all(x.isalpha() or x.isspace() for x in value):
            raise forms.ValidationError(
                "O campo: '{}' deve conter apenas letras!".format(self.label)
            )
        value.upper()


class AccountForm(forms.ModelForm):

    username = forms.CharField(max_length=100, label="Usuario")
    email = forms.EmailField(max_length=200, label="Email")
    password = forms.CharField(max_length=40, label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(
        max_length=40,
        label="Confirmacao da Senha",
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)

        helper = self.helper = FormHelper()
        helper.form_class = 'form-horizontal col-lg-10 registerForm'
        helper.label_class = 'col-sm-4'
        helper.field_class = 'col-sm-8'
        helper.form_tag = False

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class AutorCadastro(forms.ModelForm):

    nome_completo = CharacterUpperField(
        max_length=100,
        label="Nome Completo",
        help_text="Apenas caracteres."
    )
    nascimento = forms.DateField(
        input_formats=['%d/%m/%Y'],
        label="Data de Nascimento",
        help_text="Formato DD/MM/AAAA",
        widget=forms.DateInput(attrs={'class': "datepicker"})
    )
    cidade = CharacterUpperField(
        max_length=200,
        label="Cidade",
        help_text="Apenas caracteres."
    )
    estado = forms.ChoiceField(
        choices=STATE_CHOICES,
        label="Estado"
    )
    telefone = forms.DecimalField(
        decimal_places=0,
        label="Telefone",
        help_text="Apenas numeros."
    )

    def __init__(self, *args, **kwargs):
        super(AutorCadastro, self).__init__(*args, **kwargs)

        helper = self.helper = FormHelper()
        helper.form_class = 'form-horizontal col-lg-10 registerForm'
        helper.label_class = 'col-sm-4'
        helper.field_class = 'col-sm-8'
        helper.form_tag = False
        helper.add_input(Submit('register', 'Cadastrar'))
        helper.add_input(Button('cancel', 'Cancelar', css_class='btn-default'))

    def clean_nascimento(self):
        data = self.cleaned_data['nascimento']
        today = date.today()
        age = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if age < 13:
            raise forms.ValidationError("Voce deve ter pelo menos 13 anos para se "
                                        "cadastrar")
        return data

    def clean_telefone(self):
        data = self.cleaned_data['telefone']
        data = str(data)
        if len(data) == 11:
            return "({}){}-{}".format(data[:2], data[2:7], data[7:])
        return "({}){}-{}".format(data[:2], data[2:6], data[6:])

    @staticmethod
    def is_valid_username(username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return True
        raise validators.ValidationError("Usuario {} ja existe".format(username))

    @staticmethod
    def is_valid_email(email):
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return True
        raise validators.ValidationError("Email '{}' ja esta cadastrado".format(email))

    class Meta:
        model = PerfilUsuario
        exclude = ('usuario',)


class LoginForm(forms.Form):

    username = forms.CharField(max_length=100, label="Login (email)")
    password = forms.CharField(max_length=100, label="Senha", widget=forms.PasswordInput)

    placeholders = {
        'username': 'joao.silva(@gmail.com)',
        'password': 'Senha'
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        helper = self.helper = FormHelper()
        helper.form_class = 'form-horizontal col-lg-10 loginForm'
        helper.label_class = 'col-sm-3'
        helper.field_class = 'col-sm-9'
        helper.layout = Layout()
        helper.add_input(Submit('login', 'Entrar'))
        helper.add_input(Button('cancel', 'Cancelar', css_class='btn-default'))
        for field_name, field in self.fields.items():
            helper.layout.append(Field(field_name, placeholder=self.placeholders[field_name]))


class ReceitaCadastro(forms.ModelForm):

    nome = forms.CharField(max_length=50, label="Nome")
    descricao = forms.CharField(max_length=300, label="Descricao")
    autor = forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(), label="Autor", widget=forms.Select())
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label="Categoria", widget=forms.Select())
    instrucao = forms.CharField(max_length=800, label="Instrucoes", widget=forms.Textarea)
    porcoes = forms.IntegerField(label="Porcoes")
    valor_nutricional = forms.IntegerField(label="Valor Nutricional")
    metodo_preparo = forms.ChoiceField(choices=PREPARO_ESCOLHAS, label="Metodo de Preparo")
    image = forms.ImageField(label="Imagem")

    def __init__(self, *args, **kwargs):
        super(ReceitaCadastro, self).__init__(*args, **kwargs)

        helper = self.helper = FormHelper()
        helper.form_class = 'form-horizontal col-lg-10 receitaCadastro'
        helper.label_class = 'col-sm-3'
        helper.field_class = 'col-sm-9'
        helper.layout = Layout()
        helper.add_input(Submit('cadastro_receita', 'Adicionar Receita'))

    class Meta:
        model = Receita


class ComentarForm(forms.ModelForm):

    nome = forms.CharField(max_length=100, label="Nome")
    comentario = forms.CharField(max_length=1000, label="Comentario", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ComentarForm, self).__init__(*args, **kwargs)

        helper = self.helper = FormHelper()
        helper.form_class = 'form-horizontal col-lg-12 commentForm'
        helper.label_class = 'col-sm-3'
        helper.field_class = 'col-sm-9'
        helper.layout = Layout()
        helper.add_input(Submit('comentar', 'Comentar'))

    class Meta:
        model = Comentario
