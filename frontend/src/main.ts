import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule as app } from './app/app.module';

platformBrowserDynamic()
  .bootstrapModule(app)
  .catch((err) => console.error(err));
