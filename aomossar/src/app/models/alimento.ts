export interface Alimento {
  id: number;
  nome: string;
  unidade_medida?: number;
  unidade?: string;
  kcal?: number;
  // ... outros campos nutricionais
}

export interface AlimentoPayload {
  nome: string;
  unidade_medida: number;
  kcal?: number | null;
  proteinas?: number | null;
  carboidratos?: number | null;
  gordura?: number | null;
  acucar?: number | null;
  unidade?: number | null; // ID da unidade se você usar tabela de unidades
}