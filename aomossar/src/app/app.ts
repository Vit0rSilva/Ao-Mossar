import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Inicial } from './componentes/inicial/inicial';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Inicial],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('aomossar');
}
