import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { PlanningService } from '../../core/services/planning.service';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../api/base/base'; 
import { Usuario } from '../../models/usuario';
// Interface opcional para tipar seus usuários

import { TipoRefeicao } from '../../models/tipoRefeicao';
import { Horario } from '../../models/horario';
import { Cardapio } from '../../models/cardapio';

@Component({
  selector: 'app-inicial',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './inicial.html',
  styleUrl: './inicial.scss'
})
export class Inicial implements OnInit{
  loading = true;
  erro = '';

  // Dados Brutos vindos da API
  todosTiposRefeicao: TipoRefeicao[] = [];
  meusHorarios: Horario[] = [];

  // Dados Processados para a View
  tiposJaConfigurados: Set<number> = new Set(); // Set é mais rápido para verificar existência
  proximoHorario: Horario | null = null;
  horarioSelecionado: Horario | null = null;

  // Controles de UI
  expandirTipos = false;
  expandirCardapios = false;

  constructor(private planningService: PlanningService) {}

  ngOnInit() {
    this.carregarDados();
  }

  carregarDados() {
    this.loading = true;
    this.erro = '';
    
    // Chama o serviço que busca Tipos e Horários em paralelo
    this.planningService.getDashboardData().subscribe({
      next: (dados) => {
        this.todosTiposRefeicao = dados.tipos;
        // Ordena os horários recebidos pela string de hora ("06:30:00", "13:00:00", etc.)
        this.meusHorarios = dados.horarios.sort((a, b) => 
          a.horario_refeicao.localeCompare(b.horario_refeicao)
        );

        this.processarDados();
        this.loading = false;
      },
      error: (err) => {
        console.error('Erro ao carregar dashboard', err);
        // Mensagem amigável para o usuário
        this.erro = 'Não foi possível carregar seu plano alimentar. Verifique sua conexão.';
        this.loading = false;
      }
    });
  }

  processarDados() {
    // Se não tiver horários, não há o que processar
    if (this.meusHorarios.length === 0) return;

    // 1. Popula o Set com os IDs dos tipos de refeição que o usuário já tem
    this.tiposJaConfigurados.clear();
    this.meusHorarios.forEach(h => this.tiposJaConfigurados.add(h.tipo_refeicao.id));

    // 2. Calcula qual é a próxima refeição do dia
    this.calcularProximaRefeicao();
  }

  calcularProximaRefeicao() {
    const agora = new Date();
    // Formata a hora atual para "HH:MM:SS" para comparar strings diretamente
    const horaAtualStr = agora.toTimeString().split(' ')[0];

    // Encontra o primeiro horário da lista ordenada que é maior que a hora atual
    this.proximoHorario = this.meusHorarios.find(h => h.horario_refeicao > horaAtualStr) || null;

    // Se não encontrou nenhum (ex: são 23h e o último horário era 20h),
    // a próxima refeição é a primeira do dia seguinte.
    if (!this.proximoHorario && this.meusHorarios.length > 0) {
       this.proximoHorario = this.meusHorarios[0];
    }

    // Define o horário selecionado inicialmente como sendo o próximo
    this.horarioSelecionado = this.proximoHorario;
  }

  // Método chamado ao clicar em um horário na timeline
  selecionarHorario(horario: Horario) {
    this.horarioSelecionado = horario;
    // Reseta a expansão de cardápios secundários ao trocar de horário
    this.expandirCardapios = false; 
  }

  // --- Métodos Auxiliares para o Template ---

  // Retorna o cardápio marcado como 'principal', ou o primeiro se nenhum estiver marcado
  getCardapioPrincipal(horario: Horario): Cardapio | undefined {
    if (!horario.cardapios || horario.cardapios.length === 0) return undefined;
    return horario.cardapios.find(c => c.principal) || horario.cardapios[0];
  }

  // Retorna todos os cardápios que NÃO são o principal
  getCardapiosSecundarios(horario: Horario): Cardapio[] {
    const principal = this.getCardapioPrincipal(horario);
    if (!principal || !horario.cardapios) return [];
    return horario.cardapios.filter(c => c.id !== principal.id);
  }

  // Formata a string "HH:MM:SS" para "HH:MM" para ficar mais bonito na tela
  formatarHora(hora: string): string {
    return hora ? hora.substring(0, 5) : '';
  }
}