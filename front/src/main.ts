import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http';
import {appConfig} from "./app/app.config"; // Nécessaire pour HTTP

bootstrapApplication(AppComponent, appConfig)
    .catch(err => console.error(err));
