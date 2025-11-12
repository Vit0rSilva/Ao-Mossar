import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import {
  FormGroup,
  FormBuilder,
  Validators,
  AbstractControl,
  ValidationErrors,
} from '@angular/forms';
import { AuthService } from '../../core/guards/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

/**
 * Validador de Senha Complexo
 * Checa todas as regras que você especificou.
 */
export function passwordValidator(
  control: AbstractControl
): ValidationErrors | null {
  const value = control.value || '';
  const errors: ValidationErrors = {};

  if (value.length < 8) {
    errors['minLength'] = true;
  }
  if (!/[A-Z]/.test(value)) {
    errors['requireUppercase'] = true;
  }
  if (!/[a-z]/.test(value)) {
    errors['requireLowercase'] = true;
  }
  if (!/[0-9]/.test(value)) {
    errors['requireNumber'] = true;
  }
  if (!/[!@#$]/.test(value)) {
    errors['requireSpecialChar'] = true;
  }

  // Retorna o objeto de erros se algum erro existir, senão null
  return Object.keys(errors).length ? errors : null;
}

@Component({
  selector: 'app-registro',
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './registro.html',
  styleUrl: './registro.scss',
})
export class Registro {
  form: FormGroup;
  loading = false;
  error: string | null = null;

  // Regex para email
  private emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  // Regex para o telefone: 55 (DDI) + 71 (DDD) + 9 (Cel) + 8 dígitos
  private telefoneRegex = /^55719[0-9]{8}$/;

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router
  ) {
    this.form = this.fb.group({
      nome: ['', Validators.required],
      email: [
        '',
        [Validators.required, Validators.pattern(this.emailRegex)],
      ],
      telefone: [
        '',
        [Validators.required, Validators.pattern(this.telefoneRegex)],
      ],
      senha: ['', [Validators.required, passwordValidator]],
    });
  }

  // --- Getters para facilitar a vida no HTML ---
  get nome() { return this.form.get('nome'); }
  get email() { return this.form.get('email'); }
  get telefone() { return this.form.get('telefone'); }
  get senha() { return this.form.get('senha'); }
  // ------------------------------------------

  /**
   * Formata o telefone enquanto o usuário digita (Máscara)
   * Formato final: +55 (71) 9XXXX-XXXX
   */
  onTelefoneInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    let value = input.value.replace(/\D/g, ''); // 1. Remove tudo que não é dígito

    // 2. Limita ao tamanho máximo (13 dígitos: 5571912345678)
    if (value.length > 13) {
      value = value.substring(0, 13);
    }

    // 3. Aplica a máscara dinamicamente
    let maskedValue = '';
    if (value.length > 0) {
      maskedValue = '+' + value.substring(0, 2); // DDI +55
    }
    if (value.length > 2) {
      maskedValue += ' (' + value.substring(2, 4); // DDD (71)
    }
    if (value.length > 4) {
      maskedValue += ') ' + value.substring(4, 5); // O '9'
    }
    if (value.length > 5) {
      // Primeiros 4 dígitos do número
      maskedValue += ' ' + value.substring(5, 9); 
    }
    if (value.length > 9) {
      // Hífen e últimos 4 dígitos
      maskedValue += '-' + value.substring(9, 13); 
    }

    // 4. Atualiza o valor no input (o que o usuário vê)
    input.value = maskedValue;
    // 5. Atualiza o valor no form control (só os números, para o backend)
    this.form.controls['telefone'].setValue(value, { emitEvent: false });
  }

  submit() {
    this.form.markAllAsTouched(); // Mostra erros em campos não tocados
    if (this.form.invalid) return;

    this.loading = true;
    this.error = null;
    const payload = this.form.value;

    this.auth.register(payload).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.message || 'Erro ao cadastrar';
      },
    });
  }
}