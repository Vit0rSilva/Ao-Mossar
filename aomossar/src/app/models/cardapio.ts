import { CardapioAlimento } from "./cardapioAlimento";

export interface Cardapio {
  id: number;
  horario_id: number;
  principal: boolean;
  cardapio_alimentos: CardapioAlimento[];
}