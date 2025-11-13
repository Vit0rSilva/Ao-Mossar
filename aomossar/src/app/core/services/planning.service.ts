// src/app/core/services/planning.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { forkJoin, map, Observable, of, switchMap } from 'rxjs';
import { environment } from '../../../environments/environment';

import { Horario } from '../../models/horario';
import { TipoRefeicao } from '../../models/tipoRefeicao';
import { HorarioPayload } from '../../models/horario';
import { CardapioPayload } from '../../models/cardapioAlimento';
import { AlimentoPayload } from '../../models/alimento';

@Injectable({ providedIn: 'root' })
export class PlanningService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {
  }

  // --- GETs existentes ---
  getDashboardData(): Observable<{ tipos: TipoRefeicao[], horarios: Horario[] }> {
    return forkJoin({
      tipos: this.http.get<{ data: TipoRefeicao[] }>(`${this.apiUrl}/tipo_refeicoes/`).pipe(map(r => r.data)),
      horarios: this.http.get<{ data: Horario[] }>(`${this.apiUrl}/horarios/usuarios/todos`).pipe(map(r => r.data))
    });
  }

  getTiposRefeicao(): Observable<TipoRefeicao[]> {
    return this.http.get<{ data: TipoRefeicao[] }>(`${this.apiUrl}/tipo_refeicoes/`)
      .pipe(map(r => r.data));
  }

  // --- Cardápios ---
  criarCardapio(payload: CardapioPayload): Observable<any> {
    return this.http.post(`${this.apiUrl}/cardapios/`, payload);
  }

  // GET cardapio by id (para edição)
  getCardapioById(cardapioId: number): Observable<any> {
    return this.http.get<{ data: any }>(`${this.apiUrl}/cardapios/${cardapioId}`).pipe(map(r => r.data));
  }

  // PUT cardapio (ex: alterar principal)
  atualizarCardapio(cardapioId: number, payload: Partial<{ principal: boolean }>): Observable<any> {
    return this.http.put(`${this.apiUrl}/cardapios/${cardapioId}`, payload);
  }

  // --- Alimentos ---
  // criar alimento (post em /alimentos/{cardapioId})
  criarAlimento(cardapioId: number, payload: AlimentoPayload): Observable<any> {
    return this.http.post(`${this.apiUrl}/alimentos/${cardapioId}`, payload);
  }

  // atualizar alimento (PUT /alimentos/{alimentoId})
  atualizarAlimento(alimentoId: number, payload: Partial<AlimentoPayload>): Observable<any> {
    return this.http.put(`${this.apiUrl}/alimentos/${alimentoId}`, payload);
  }

  // deletar alimento (DELETE /alimentos/{alimentoId})
  deletarAlimento(alimentoId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/alimentos/${alimentoId}`);
  }

  // --- Outros métodos já existentes (horários, salvar fluxo) ---
  criarHorario(payload: HorarioPayload): Observable<any> {
    return this.http.post(`${this.apiUrl}/horarios/`, payload);
  }

  // Exemplo: salvar novo cardapio com alimentos (usado no fluxo de criação)
  salvarNovoCardapio(horarioId: number, alimentos: AlimentoPayload[]): Observable<any> {
    const cardapioPayload: CardapioPayload = {
      horario_id: horarioId,
      principal: true
    };

    return this.criarCardapio(cardapioPayload).pipe(
      switchMap((respCardapio: any) => {
        if (alimentos.length === 0) return of(respCardapio);
        const novoCardapioId = respCardapio.data?.id || respCardapio.id;
        const requestsAlimentos = alimentos.map(alimento =>
          this.criarAlimento(novoCardapioId, alimento)
        );
        return forkJoin(requestsAlimentos).pipe(map(() => respCardapio));
      })
    );
  }

  // Fluxo completo de criação de horário + cardapio + alimentos (já existente no seu código)
  salvarPlanejamentoCompleto(
    horarioPayload: HorarioPayload,
    criarCardapio: boolean,
    alimentos: AlimentoPayload[]
  ): Observable<any> {
    return this.criarHorario(horarioPayload).pipe(
      switchMap((respHorario: any) => {
        if (!criarCardapio || alimentos.length === 0) {
          return of(respHorario);
        }
        const novoHorarioId = respHorario.data?.id || respHorario.id;
        const cardapioPayload: CardapioPayload = {
          horario_id: novoHorarioId,
          principal: true
        };
        return this.criarCardapio(cardapioPayload).pipe(
          switchMap((respCardapio: any) => {
            const novoCardapioId = respCardapio.data?.id || respCardapio.id;
            const requestsAlimentos = alimentos.map(alimento =>
              this.criarAlimento(novoCardapioId, alimento)
            );
            return forkJoin(requestsAlimentos).pipe(map(() => respHorario));
          })
        );
      })
    );
  }
}
