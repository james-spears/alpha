import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UploadComponent } from './upload/upload.component';
import { SettingsComponent } from './settings/settings.component';
import { HelpComponent } from './help/help.component';


const routes: Routes = [
  { path: "upload", component: UploadComponent },
  { path: "settings", component: SettingsComponent },
  { path: "help", component: HelpComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
