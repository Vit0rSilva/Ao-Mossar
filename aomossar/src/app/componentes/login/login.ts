import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../core/guards/auth.service';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  form: FormGroup;
  loading = false;
  error: string | null = null;

  constructor(private fb: FormBuilder, private auth: AuthService, private router: Router) {
    // CORREÇÃO: Inicializar o form dentro do construtor para garantir que 'fb' já existe
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      senha: ['', Validators.required]
    });
  }

  submit() {
    if (this.form.invalid) return;

    this.loading = true;
    this.error = null;

    // CORREÇÃO: Desestruturar para pegar email e senha separadamente
    const { email, senha } = this.form.value;

    // CORREÇÃO: Passar os dois argumentos conforme esperado pelo AuthService
    this.auth.login(email, senha).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/']); // Redireciona para a home após login
      },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.message || 'Erro ao efetuar login';
        console.error('Erro Login:', err);
      }
    });
  }
}