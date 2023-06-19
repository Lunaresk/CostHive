import {Component, OnInit, OnDestroy} from '@angular/core';
import {Subscription} from 'rxjs';
import {UsersApiService} from './users-api.service';
import {User} from './user.model';

@Component({
  selector: 'app-root',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit, OnDestroy {
  title = 'app';
  usersListSubs: Subscription;
  usersList: User[];

  constructor(private usersApi: UsersApiService) {
    this.usersListSubs = new Subscription;
    this.usersList = []
  }

  ngOnInit() {
    this.usersListSubs = this.usersApi
      .getExams()
      .subscribe((res: User[]) => {
          console.log(res);
          this.usersList = res;
        },
        console.error
      );
  }

  ngOnDestroy() {
    this.usersListSubs.unsubscribe();
  }
}