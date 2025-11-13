// src/app/features/cardapio/cardapio.ts  (ou cardapio.component.ts conforme seu padrão)
import { Component, OnInit } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { PlanningService } from '../../core/services/planning.service';
import { AlimentoPayload } from '../../models/alimento';
import { switchMap, forkJoin, of } from 'rxjs';

@Component({
  selector: 'app-cardapio',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './cardapio.html',
  styleUrl: './cardapio.scss',
})
export class Cardapio implements OnInit {
  // Form usado para adicionar novo alimento (criação rápida)
  formAlimento: FormGroup;

  // Form usado para editar alimento existente (modal)
  formEditAlimento: FormGroup;

  listaAlimentos: Array<Partial<AlimentoPayload & { id?: number }>> = []; // pode conter itens com id (existentes) ou sem id (novos)
  enviando = false;
  erro = '';

  horarioId: number | null = null;
  // Quando em modo de edição:
  editMode = false;
  cardapioId: number | null = null;
  cardapioPrincipal = false;

  // controle modais
  mostrarModalEditar = false;
  alimentoEditando: Partial<AlimentoPayload & { id?: number }> | null = null;

  // modal confirmar delete
  mostrarModalExcluir = false;
  alimentoParaExcluir: Partial<AlimentoPayload & { id?: number }> | null = null;

  constructor(
    private fb: FormBuilder,
    private planningService: PlanningService,
    private router: Router,
    private route: ActivatedRoute,
    private location: Location
  ) {
    this.formAlimento = this.fb.group({
      nome: ['', Validators.required],
      unidade_medida: [null, [Validators.required, Validators.min(1)]],
      kcal: [null],
      proteinas: [null],
      carboidratos: [null],
      gordura: [null]
    });

    this.formEditAlimento = this.fb.group({
      nome: ['', Validators.required],
      unidade_medida: [null, [Validators.required, Validators.min(1)]],
      kcal: [null],
      proteinas: [null],
      carboidratos: [null],
      gordura: [null]
    });
  }

  ngOnInit() {
    // Detecta se a rota veio com cardapioId -> modo edição
    const cardapioIdParam = this.route.snapshot.paramMap.get('cardapioId');
    const horarioIdParam = this.route.snapshot.paramMap.get('horarioId');

    if (cardapioIdParam) {
      // EDIÇÃO
      this.editMode = true;
      this.cardapioId = Number(cardapioIdParam);
      this.carregarCardapioParaEdicao(this.cardapioId);
    } else if (horarioIdParam) {
      // CRIAÇÃO
      this.horarioId = Number(horarioIdParam);
    } else {
      this.erro = 'ID do horário ou do cardápio não foi informado na rota.';
    }
  }

  // --- EDIÇÃO: busca o cardápio e popula lista ---
  carregarCardapioParaEdicao(cardapioId: number) {
    this.enviando = true;
    this.planningService.getCardapioById(cardapioId).subscribe({
      next: (data: any) => {
        // API retornou o "data" conforme seu exemplo
        this.enviando = false;
        if (!data) {
          this.erro = 'Cardápio não encontrado.';
          return;
        }
        this.cardapioId = data.id;
        this.horarioId = data.horario_id;
        this.cardapioPrincipal = !!data.principal;

        // Mapeia cardapio_alimentos para lista (mantendo id se existir)
        this.listaAlimentos = (data.cardapio_alimentos || []).map((ca: any) => {
          const alim = ca.alimento || {};
          return {
            id: ca.id, // id do relacionamento alimento no cardápio (ou id do registro que sua API usa)
            alimento_id: ca.alimento_id,
            nome: alim.nome || '',
            unidade_medida: alim.unidade_medida || null,
            kcal: alim.kcal || null,
            proteinas: alim.proteinas || null,
            carboidratos: alim.carboidratos || null,
            gordura: alim.gordura || null
          } as Partial<AlimentoPayload & { id?: number }>;
        });
      },
      error: (err) => {
        console.error('Erro ao carregar cardápio', err);
        this.erro = 'Erro ao carregar cardápio para edição.';
        this.enviando = false;
      }
    });
  }

  // --- ADD / REMOVER locais (front) ---
  adicionarAlimento() {
    if (this.formAlimento.invalid) return;
    const novo: Partial<AlimentoPayload> = this.formAlimento.value;
    // quando criar em modo edição, não tem id ainda — será criado no salvar
    this.listaAlimentos.push(novo);
    this.formAlimento.reset();
  }

  removerAlimento(index: number) {
    // Se estivermos em edição e o item tem id (já persistido), abrir modal confirmar exclusão
    const item = this.listaAlimentos[index];
    if (this.editMode && item && item.id) {
      this.alimentoParaExcluir = item;
      this.mostrarModalExcluir = true;
      // guarda o index para remover após exclusão
      (this.alimentoParaExcluir as any).__index = index;
      return;
    }
    // senão, só remove da lista (não persistido)
    this.listaAlimentos.splice(index, 1);
  }

  // --- MODAL editar alimento (abre preenchido) ---
  abrirModalEditar(item: Partial<AlimentoPayload & { id?: number }>) {
    this.alimentoEditando = item;
    // preenche formEdit com os dados do item
    this.formEditAlimento.patchValue({
      nome: item.nome || '',
      unidade_medida: item.unidade_medida || null,
      kcal: item.kcal || null,
      proteinas: item.proteinas || null,
      carboidratos: item.carboidratos || null,
      gordura: item.gordura || null
    });
    this.mostrarModalEditar = true;
  }

  salvarEdicaoAlimento() {
    if (!this.alimentoEditando) return;
    if (this.formEditAlimento.invalid) return;

    const valores = this.formEditAlimento.value;
    // Atualiza o objeto local
    Object.assign(this.alimentoEditando, valores);
    this.mostrarModalEditar = false;
    this.alimentoEditando = null;
    // Não persistimos ainda — o persist será feito no salvarCardapio (PUT/POST em lote)
  }

  cancelarEditar() {
    this.mostrarModalEditar = false;
    this.alimentoEditando = null;
  }

  // --- Exclusão confirmada (após modal) ---
  confirmarExcluirAlimento() {
    if (!this.alimentoParaExcluir) return;
    const idx = (this.alimentoParaExcluir as any).__index;
    const item = this.alimentoParaExcluir;
    if (this.editMode && item && item.id) {
      // chama API DELETE
      this.planningService.deletarAlimento(item.id as number).subscribe({
        next: () => {
          // remove do array local
          if (typeof idx === 'number') {
            this.listaAlimentos.splice(idx, 1);
          } else {
            // fallback: buscar e remover por id
            const pos = this.listaAlimentos.findIndex(a => a.id === item.id);
            if (pos >= 0) this.listaAlimentos.splice(pos, 1);
          }
          this.mostrarModalExcluir = false;
          this.alimentoParaExcluir = null;
        },
        error: (err) => {
          console.error('Erro ao excluir alimento', err);
          alert('Não foi possível excluir o alimento.');
          this.mostrarModalExcluir = false;
          this.alimentoParaExcluir = null;
        }
      });
    } else {
      // não persistido, só remove local
      if (typeof idx === 'number') {
        this.listaAlimentos.splice(idx, 1);
      } else {
        const pos = this.listaAlimentos.findIndex(a => a === item);
        if (pos >= 0) this.listaAlimentos.splice(pos, 1);
      }
      this.mostrarModalExcluir = false;
      this.alimentoParaExcluir = null;
    }
  }

  cancelarExcluir() {
    this.mostrarModalExcluir = false;
    this.alimentoParaExcluir = null;
  }

  // --- SALVAR CARDÁPIO (CRIA ou ATUALIZA) ---
  salvarCardapio() {
    if (this.listaAlimentos.length === 0) {
      this.erro = 'Adicione pelo menos um alimento.';
      return;
    }
    if (!this.horarioId && !this.cardapioId) {
      this.erro = 'ID do horário/cardápio não encontrado.';
      return;
    }

    this.enviando = true;
    this.erro = '';

    if (this.editMode && this.cardapioId) {
      // Atualizar: para cada alimento => se tem id -> PUT, se não -> POST para /alimentos/{cardapioId}
      const requests = this.listaAlimentos.map(item => {
        if (item.id) {
          // PUT /alimentos/{id} - payload com campos editáveis (nome, unidade_medida, kcal, etc)
          const payload: Partial<AlimentoPayload> = {
            nome: item.nome,
            unidade_medida: item.unidade_medida,
            kcal: item.kcal,
            proteinas: item.proteinas,
            carboidratos: item.carboidratos,
            gordura: item.gordura
          };
          return this.planningService.atualizarAlimento(item.id as number, payload);
        } else {
          // POST /alimentos/{cardapioId}
          const payload: AlimentoPayload = {
            nome: item.nome as string,
            unidade_medida: item.unidade_medida as number,
            kcal: item.kcal ?? null,
            proteinas: item.proteinas ?? null,
            carboidratos: item.carboidratos ?? null,
            gordura: item.gordura ?? null
          };
          return this.planningService.criarAlimento(this.cardapioId as number, payload);
        }
      });

      // executa todas as requests
      forkJoin(requests).subscribe({
        next: () => {
          this.enviando = false;
          alert('Cardápio atualizado com sucesso!');
          this.router.navigate(['/']); // volta ao dashboard
        },
        error: (err) => {
          console.error('Erro ao atualizar cardápio', err);
          this.erro = 'Erro ao atualizar cardápio.';
          this.enviando = false;
        }
      });

    } else {
      // Fluxo de criação (já existente) — usa salvarNovoCardapio para criar cardapio e alimentos
      this.planningService.salvarNovoCardapio(this.horarioId as number, this.listaAlimentos as AlimentoPayload[])
        .subscribe({
          next: () => {
            this.enviando = false;
            alert('Cardápio salvo com sucesso!');
            this.router.navigate(['/']);
          },
          error: (err) => {
            console.error('Erro ao salvar cardápio', err);
            this.erro = 'Erro ao salvar cardápio.';
            this.enviando = false;
          }
        });
    }
  }

  voltar() {
    this.location.back();
  }
}
