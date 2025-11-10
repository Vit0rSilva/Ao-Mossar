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
  //private apiUrl = environment.apiUrl;
  private apiUrl = 'https://algumacoisa-python.gdaxye.easypanel.host'; 

  constructor(private http: HttpClient) { 
      console.log('🚀 PlanningService INICIADO com URL FORÇADA:', this.apiUrl);
  }

  // --- Métodos de LEITURA (GET) ---
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

  // --- Métodos de CRIAÇÃO (POST) ---

  criarHorario(payload: HorarioPayload): Observable<any> {
    return this.http.post(`${this.apiUrl}/horarios/`, payload);
  }

  criarCardapio(payload: CardapioPayload): Observable<any> {
    return this.http.post(`${this.apiUrl}/cardapios/`, payload);
  }

  criarAlimento(cardapioId: number, payload: AlimentoPayload): Observable<any> {
    // URL conforme solicitado: /alimentos/{cardapio_id}
    // O payload vai no corpo da requisição
    return this.http.post(`${this.apiUrl}/alimentos/${cardapioId}`, payload);
  }

  // --- FLUXO DE SALVAMENTO EM CADEIA ---
  salvarPlanejamentoCompleto(
    horarioPayload: HorarioPayload,
    criarCardapio: boolean,
    alimentos: AlimentoPayload[]
  ): Observable<any> {
    // 1. Envia Horário
    return this.criarHorario(horarioPayload).pipe(
      switchMap((respHorario: any) => {
        // Se não quis cardápio OU não adicionou alimentos, o fluxo termina aqui.
        if (!criarCardapio || alimentos.length === 0) {
          return of(respHorario); // Retorna observable que completa imediatamente
        }

        // ID do horário recém-criado (verifique se sua API retorna 'id' dentro de 'data')
        // Ajuste aqui se sua API retornar diferente (ex: respHorario.id direto)
        const novoHorarioId = respHorario.data?.id || respHorario.id;

        const cardapioPayload: CardapioPayload = {
          horario_id: novoHorarioId,
          principal: true
        };

        // 2. Envia Cardápio (usando o ID do horário)
        return this.criarCardapio(cardapioPayload).pipe(
          switchMap((respCardapio: any) => {
            const novoCardapioId = respCardapio.data?.id || respCardapio.id;

            // 3. Envia TODOS os alimentos (usando o ID do cardápio)
            // Cria um array de Observables, um para cada request de alimento
            const requestsAlimentos = alimentos.map(alimento =>
              this.criarAlimento(novoCardapioId, alimento)
            );

            // forkJoin executa todos em paralelo e espera todos terminarem
            return forkJoin(requestsAlimentos).pipe(
              // Retorna a resposta do horário original para manter consistência
              map(() => respHorario)
            );
          })
        );
      })
    );
  }
  salvarNovoCardapio(
    horarioId: number,
    alimentos: AlimentoPayload[]
  ): Observable<any> {
    // 1. Cria o Cardápio
    const cardapioPayload: CardapioPayload = {
      horario_id: horarioId,
      // Nota: Sua API de exemplo enviou 'true'.
      // Você pode querer uma lógica no backend para gerenciar
      // qual cardápio é o principal se já existir um.
      principal: true
    };

    return this.criarCardapio(cardapioPayload).pipe(
      switchMap((respCardapio: any) => {
        // Se não houver alimentos, paramos aqui
        if (alimentos.length === 0) {
          return of(respCardapio);
        }

        const novoCardapioId = respCardapio.data?.id || respCardapio.id;

        // 2. Cria TODOS os alimentos em paralelo vinculados ao Cardápio
        const requestsAlimentos = alimentos.map(alimento =>
          this.criarAlimento(novoCardapioId, alimento)
        );

        // forkJoin espera todos os alimentos serem criados
        return forkJoin(requestsAlimentos).pipe(
          map(() => respCardapio) // Retorna a resposta do cardápio
        );
      })
    );
  }
}