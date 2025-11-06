// componentes/inicial/inicial.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UsuarioService } from '../../core/services/usuario.service'; 
import { Usuario } from '../../models/usuario';

@Component({
  selector: 'app-inicial',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicial.html',
  styleUrl: './inicial.scss',
})
export class Inicial implements OnInit {
  usuarios: Usuario[] = [];
  carregando: boolean = true;
  erro: string = '';
  mostrarModal: boolean = false;
  mensagemModal: string = '';

  constructor(private usuarioService: UsuarioService) {
    console.log('✅ Componente Inicial construído'); // Debug
  }

  ngOnInit() {
    console.log('✅ ngOnInit executado'); // Debug
    this.carregarUsuarios();
  }

  carregarUsuarios(): void {
    console.log('✅ Carregando usuários...'); // Debug
    this.carregando = true;
    this.usuarioService.getUsuarios().subscribe({
      next: (response) => {
        console.log('✅ Resposta da API:', response); // Debug
        if (response.success) {
          this.usuarios = response.data;
          console.log('✅ Usuários carregados:', this.usuarios); // Debug
        } else {
          this.erro = response.message;
          console.log('❌ Erro na resposta:', this.erro); // Debug
        }
        this.carregando = false;
      },
      error: (error) => {
        console.error('❌ Erro na requisição:', error); // Debug
        this.erro = 'Erro ao carregar usuários';
        this.carregando = false;
      }
    });
  }

  selecionarUsuario(usuario: Usuario): void {
    console.log('✅ Usuário selecionado:', usuario); // Debug
    this.usuarioService.salvarUsuarioSelecionado(usuario);
    this.mensagemModal = `Perfil ${usuario.nome} selecionado com sucesso!`;
    this.mostrarModal = true;
    
    setTimeout(() => {
      this.fecharModal();
    }, 2000);
  }

  fecharModal(): void {
    this.mostrarModal = false;
  }

  gerarAvatar(nome: string): string {
    const iniciais = nome.charAt(0).toUpperCase();
    return `https://via.placeholder.com/150/007bff/ffffff?text=${iniciais}`;
  }
}