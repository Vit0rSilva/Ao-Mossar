import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
// Certifique-se de que o caminho para seu environment está correto
import { environment } from '../../../environments/environment';


interface LoginResponse {
    success: boolean;
    message: string;
    data: {
        access_token: string;
        token_type: string;
        expires_in: number;
    };
}

@Injectable({ providedIn: 'root' })
export class AuthService {
    private baseUrl = environment.apiUrl + '/usuarios';

    constructor(private http: HttpClient) { }

    login(email: string, senha: string): Observable<LoginResponse> {
        return this.http.post<LoginResponse>(`${this.baseUrl}/login`, { email, senha }).pipe(
            tap(resp => {
                if (resp && resp.success && resp.data?.access_token) {
                    // É recomendável salvar o token com um nome padrão
                    localStorage.setItem('access_token', resp.data.access_token);
                }
            })
        );
    }

    register(payload: { email: string; nome: string; telefone: string; senha: string }) {
        return this.http.post(`${this.baseUrl}/`, payload);
    }

    logout() {
        localStorage.removeItem('access_token');
    }

    getToken() {
        return localStorage.getItem('access_token');
    }

    // Método útil para verificar se o usuário está logado
    estaLogado(): boolean {
        return !!this.getToken();
    }
}