import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnInit {
  srcResult: any;
  fileName: string;
  upload: ArrayBuffer;
  constructor() { }

  ngOnInit() {
  }

  onFileSelected() {
    const inputNode: any = document.querySelector('#file');
  
    if (typeof (FileReader) !== 'undefined') {
      const reader = new FileReader();
  
      reader.onload = (e: any) => {
        this.srcResult = e.target.result;
        console.log(this.srcResult);
      };
      this.fileName = inputNode.files[0].name
      reader.readAsArrayBuffer(inputNode.files[0]);
    }
  }

  

}
