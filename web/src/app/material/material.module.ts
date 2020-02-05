import { NgModule } from '@angular/core';
import { MatButtonModule, MatFormFieldModule, MatInputModule } from '@angular/material';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';

const MaterialComponent = [
  MatButtonModule,
  MatMenuModule,
  MatIconModule,
  MatFormFieldModule,
  MatInputModule
];

@NgModule({
  imports: [
    MaterialComponent,
  ],
  exports: [
    MaterialComponent,
  ],
})
export class MaterialModule { }
