import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http'; // Nécessaire pour HTTP

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(), // Ajout du HttpClientModule
  ],
}).catch((err) => console.error(err));
