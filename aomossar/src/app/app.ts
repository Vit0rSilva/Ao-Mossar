import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Inicial } from './componentes/inicial/inicial';
import { Login } from './componentes/login/login';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('aomossar');
}
