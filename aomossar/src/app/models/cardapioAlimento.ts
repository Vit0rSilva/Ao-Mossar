import { Alimento } from "./alimento";

export interface CardapioAlimento {
  id: number;
  alimento: Alimento;
  // quantidade poderia estar aqui se fosse diferente da unidade padrão do alimento
}

export interface CardapioPayload {
  horario_id: number;
  principal: boolean;
}