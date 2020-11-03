import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { Tag } from '../classes/tag';
import { Keyword } from '../classes/keyword';
import { Blog } from '../classes/blog';
import { Shop } from '../classes/shop';

@Component({
  selector: 'app-search',
  templateUrl: './search.page.html',
  styleUrls: ['./search.page.scss'],
})
export class SearchPage implements OnInit {
  public doShow: boolean = false;
  public keywordForm: FormGroup;
  public tags: Tag[] = [];
  public keywords: Keyword[] = [];
  public blogs: Blog[] = [];
  public shops: Shop[] = [];
  public BASE_URL: string = 'http://127.0.0.1:5000';
  public POPULAR_URL = this.BASE_URL + '/getPopularlists';
  public KEYWORD_URL = this.BASE_URL + '/relatedKeywords?keyword=';
  public BLOG_URL = this.BASE_URL + '/getBlogs?keyword=';
  public SHOP_URL = this.BASE_URL + '/getShops?keyword=';

  constructor(private http: HttpClient,
    private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.keywordForm = this.formBuilder.group({
      keyword: [null, [Validators.required, Validators.minLength(2)]]
    });
    this.http.get(this.POPULAR_URL)
    .subscribe((result) => {
      this.tags = <Tag[]>result;
      this.keywordForm.setValue({'keyword': this.tags[0].name });
    }, error => {
      alert(JSON.stringify(error));
    });
  }
  getKeywordErrorMessage() {
    return this.keywordForm.controls.keyword.hasError('required') ? "키워드를 입력하세요." :
        this.keywordForm.controls.keyword.hasError('minlength') ? "최소 2자 이상 입력해야 합니다." :
            '';
  }
  setSearchTerm(term) {
    this.keywordForm.setValue({'keyword': term });
  }
  submitForm() {
    this.doShow = true;  
    var keyword = this.keywordForm.value.keyword.replaceAll(" ", "");
    
    this.http.get(this.KEYWORD_URL+keyword)
    .subscribe((result) => {
      this.keywords = <Keyword[]>result;
    }, error => {
      alert(JSON.stringify(error));
    });  

    this.http.get(this.BLOG_URL+keyword)
    .subscribe((result) => {
      console.log(result)
      this.blogs = <Blog[]>result;
    }, error => {
      alert(JSON.stringify(error));
    }); 

    this.http.get(this.SHOP_URL+keyword)
    .subscribe((result) => {
      this.shops = <Shop[]>result;
    }, error => {
      alert(JSON.stringify(error));
    });    
  }     
  
  openlink(path: string) {
    window.open(path, '_blank');
  }
  
}
