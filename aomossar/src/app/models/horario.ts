import { TipoRefeicao } from "./tipoRefeicao";
import { Cardapio } from "./cardapio";

export interface Horario {
  id: number;
  usuario_id: string;
  tipo_refeicao_id: number;
  horario_refeicao: string; // Formato "HH:MM:SS"
  tipo_refeicao: TipoRefeicao;
  cardapios: Cardapio[];
  // Campos auxiliares para o frontend
  jaPassou?: boolean;
}

export interface HorarioPayload {
  usuario_id: string;
  tipo_refeicao_id: number;
  horario_refeicao: string;
}