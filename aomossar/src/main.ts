import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config'; // 1. Importe seu config
import { App } from './app/app';

// 3. Passe o 'appConfig' como segundo argumento
bootstrapApplication(App, appConfig) 
  .catch((err) => console.error(err));