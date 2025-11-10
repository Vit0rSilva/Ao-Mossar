// features/usuarios/models/usuario.model.ts
export interface Usuario {
  id: string;
  nome: string;
  telefone: string;
  email: string;
  senha: string;
}

export interface UsuarioResponse {
  success: boolean;
  message: string;
  data: Usuario[];
}