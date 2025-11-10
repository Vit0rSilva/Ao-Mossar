// services/usuario.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UsuarioResponse, Usuario } from '../../models/usuario';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UsuarioService {
  private http = inject(HttpClient); // ✅ Método moderno com inject()
  private apiUrl = environment.apiUrl + '/usuarios';

  getUsuarios(): Observable<UsuarioResponse> {
    return this.http.get<UsuarioResponse>(this.apiUrl);
  }

  salvarUsuarioSelecionado(usuario: Usuario): void {
    localStorage.setItem('usuarioSelecionado', JSON.stringify(usuario));
    console.log('Usuário salvo no localStorage:', usuario);
  }

  getUsuarioSelecionado(): Usuario | null {
    const usuario = localStorage.getItem('usuarioSelecionado');
    return usuario ? JSON.parse(usuario) : null;
  }
}