import { Routes } from '@angular/router';
import { Inicial } from './componentes/inicial/inicial';
import { Login } from './componentes/login/login';
import { Registro } from './componentes/registro/registro';
import { Horarios } from './componentes/horarios/horarios'; 
import { Cardapio } from './componentes/cardapio/cardapio';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
    // Rota protegida: só entra se o authGuard permitir
    { path: '', component: Inicial, canActivate: [authGuard], pathMatch: 'full' },
    { path: 'login', component: Login },
    { path: 'register', component: Registro },
    { path: 'adicionar/horario', component: Horarios,  canActivate: [authGuard], pathMatch: 'full' },
    { path: 'cardapio/editar/:cardapioId', component: Cardapio },
    { path: 'adicionar/cardapio/:horarioId', component: Cardapio,  canActivate: [authGuard], pathMatch: 'full' },
    // Qualquer outra rota desconhecida redireciona para home (que vai jogar pro login se não tiver auth)
    { path: '**', redirectTo: '' }
];