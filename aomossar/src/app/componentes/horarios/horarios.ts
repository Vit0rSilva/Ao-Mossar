import { Component, OnInit } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormArray } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { PlanningService } from '../../core/services/planning.service';
import { TipoRefeicao } from '../../models/tipoRefeicao';
import { AlimentoPayload } from '../../models/alimento';

@Component({
  selector: 'app-horarios',
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './horarios.html',
  styleUrl: './horarios.scss',
})
export class Horarios implements OnInit{
  formHorario: FormGroup;
  formAlimento: FormGroup;
  
  tiposRefeicao: TipoRefeicao[] = [];
  listaAlimentos: AlimentoPayload[] = []; // Lista local temporária
  
  loading = false;
  enviando = false;
  erro = '';

  constructor(
    private fb: FormBuilder,
    private planningService: PlanningService,
    private router: Router,
    private location: Location
  ) {
    // Formulário principal (Horário)
    this.formHorario = this.fb.group({
      horario: ['', Validators.required],
      tipo_refeicao_id: [null, Validators.required],
      criar_cardapio: [true] // Checkbox para saber se deseja vincular cardápio agora
    });

    // Formulário para adicionar UM alimento por vez à lista
    this.formAlimento = this.fb.group({
      nome: ['', Validators.required],
      unidade_medida: [null, [Validators.required, Validators.min(1)]],
      // Campos opcionais nutricionais
      kcal: [null],
      proteinas: [null],
      carboidratos: [null],
      gordura: [null]
    });
  }

  ngOnInit() {
    this.carregarTipos();
  }

  carregarTipos() {
    this.loading = true;
    this.planningService.getTiposRefeicao().subscribe({
      next: (tipos) => {
        this.tiposRefeicao = tipos;
        this.loading = false;
      },
      error: (err) => {
        this.erro = 'Erro ao carregar tipos de refeição.';
        this.loading = false;
      }
    });
  }

  // --- Manipulação da Lista Local de Alimentos ---
  adicionarAlimento() {
    if (this.formAlimento.invalid) return;

    const novoAlimento: AlimentoPayload = this.formAlimento.value;
    this.listaAlimentos.push(novoAlimento);
    
    // Limpa o form para o próximo
    this.formAlimento.reset();
  }

  removerAlimento(index: number) {
    this.listaAlimentos.splice(index, 1);
  }

  // --- Envio Final ---
  salvarTudo() {
    if (this.formHorario.invalid) return;

    this.enviando = true;
    this.erro = '';

    // Pega ID do usuário (ajuste conforme sua autenticação real)
    // const usuarioId = localStorage.getItem('usuario_id'); 
    // Se estiver usando seu AuthService, pode ser this.auth.getUserId()
    // Vou usar um valor fixo baseado no seu exemplo JSON anterior se não tiver no localStorage
    const usuarioId = localStorage.getItem('usuario_id') || 'aa0eb083-91f1-46c7-9521-80f97cfe1938'; 

    const horarioPayload = {
      usuario_id: usuarioId,
      tipo_refeicao_id: Number(this.formHorario.value.tipo_refeicao_id),
      // Adiciona segundos para ficar no formato HH:MM:SS se o input type="time" só der HH:MM
      horario_refeicao: this.formHorario.value.horario + ':00' 
    };

    const desejaCriarCardapio = this.formHorario.value.criar_cardapio;

    this.planningService.salvarPlanejamentoCompleto(
      horarioPayload,
      desejaCriarCardapio,
      this.listaAlimentos
    ).subscribe({
      next: () => {
        alert('Planejamento salvo com sucesso!');
        this.router.navigate(['/']); // Volta para o dashboard inicial
      },
      error: (err) => {
        console.error(err);
        this.erro = 'Ocorreu um erro ao salvar. Tente novamente.';
        this.enviando = false;
      }
    });
  }

  voltar() {
    this.location.back();
  }
}
