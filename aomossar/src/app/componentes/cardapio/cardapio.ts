import { Component, OnInit} from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormArray } from '@angular/forms';
import { ActivatedRoute,Router, RouterModule } from '@angular/router';
import { PlanningService } from '../../core/services/planning.service';
import { TipoRefeicao } from '../../models/tipoRefeicao';
import { AlimentoPayload } from '../../models/alimento';


@Component({
  selector: 'app-cardapio',
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  standalone: true,
  templateUrl: './cardapio.html',
  styleUrl: './cardapio.scss',
})
export class Cardapio implements OnInit{
formAlimento: FormGroup;
  
  listaAlimentos: AlimentoPayload[] = [];
  
  enviando = false;
  erro = '';
  horarioId: number | null = null;

  constructor(
    private fb: FormBuilder,
    private planningService: PlanningService,
    private router: Router,
    private route: ActivatedRoute, // Para ler o ID da URL
    private location: Location
  ) {
    // Reutilizamos exatamente o mesmo formulário de alimentos
    this.formAlimento = this.fb.group({
      nome: ['', Validators.required],
      unidade_medida: [null, [Validators.required, Validators.min(1)]],
      kcal: [null],
      proteinas: [null],
      carboidratos: [null],
      gordura: [null]
    });
  }

  ngOnInit() {
    // Captura o ID do horário vindo da rota
    const id = this.route.snapshot.paramMap.get('horarioId');
    if (id) {
      this.horarioId = Number(id);
    } else {
      this.erro = 'ID do horário não encontrado. Volte e tente novamente.';
    }
  }

  // --- Reutilização da Lógica de Lista de Alimentos ---
  adicionarAlimento() {
    if (this.formAlimento.invalid) return;

    const novoAlimento: AlimentoPayload = this.formAlimento.value;
    this.listaAlimentos.push(novoAlimento);
    
    this.formAlimento.reset(); // Limpa para o próximo
  }

  removerAlimento(index: number) {
    this.listaAlimentos.splice(index, 1);
  }

  // --- Envio Final ---
  salvarCardapio() {
    if (!this.horarioId || this.listaAlimentos.length === 0) {
      this.erro = 'Você precisa adicionar pelo menos um alimento ao cardápio.';
      return;
    }

    this.enviando = true;
    this.erro = '';

    this.planningService.salvarNovoCardapio(
      this.horarioId,
      this.listaAlimentos
    ).subscribe({
      next: () => {
        alert('Cardápio salvo com sucesso!');
        this.router.navigate(['/']); // Volta para o dashboard inicial
      },
      error: (err) => {
        console.error(err);
        this.erro = 'Ocorreu um erro ao salvar o cardápio.';
        this.enviando = false;
      }
    });
  }

  voltar() {
    this.location.back();
  }
}
