// features/usuarios/models/usuario.model.ts
export interface Usuario {
  id: number;
  nome: string;
  telefone: string;
}

export interface UsuarioResponse {
  success: boolean;
  message: string;
  data: Usuario[];
}