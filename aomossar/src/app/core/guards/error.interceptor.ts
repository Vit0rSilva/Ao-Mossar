import { Injectable, inject } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';
import { AuthService } from './auth.service';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
    // Usando 'inject' para ficar moderno como seu outro service
    private authService = inject(AuthService);
    private router = inject(Router);

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return next.handle(request).pipe(
            catchError((err: HttpErrorResponse) => {
                // Verifica se o erro é 401 (Não autorizado - token expirado/inválido)
                // ou 403 (Proibido - token válido, mas sem permissão)
                if ([401, 403].includes(err.status)) {
                    // Se for 401/403, desconecta o usuário automaticamente
                    this.authService.logout();
                    
                    // Redireciona para a página de login
                    this.router.navigate(['/login']);
                }

                // Repassa o erro para que o componente também saiba que falhou
                // (ex: para parar um loading spinner)
                return throwError(() => err);
            })
        );
    }
}