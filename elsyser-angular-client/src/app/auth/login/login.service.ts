import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';

import { IUser } from '../../interfaces/IUser';

@Injectable()

export class LoginService {
    private _loginUrl = 'api-token-auth/';

    constructor(private _http: Http) { }

    loginUser(body: Object): Observable<IUser> {
        let bodyString = JSON.stringify(body); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        return this._http.post(this._loginUrl, bodyString, options)
                         .map((res: Response) => res.json())
                         .catch((error: any) => Observable.throw(error.json() || 'Server error'));
    }
}