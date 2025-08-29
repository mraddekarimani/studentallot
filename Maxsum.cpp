#include <bits/stdc++.h>
using namespace std;

int main(){
    int n;
    cout<<"enter size of array";
    cin>>n;
    vector<int>arr(n);
    for(int i=0;i<n;i++){
        cin>>arr[i];
    }

    int csum=0;
    int maxsum=0;
    int l=0,r=0;
    unordered_set<int>seen;
     while(r<n){
        while(seen.count(arr[r])){
            seen.erase(arr[l]);
            csum-=arr[l];
            l++;
        }
        seen.insert(arr[r]);
        csum+=arr[r];
        maxsum=max(maxsum,csum);
        r++;
     }
     cout<<maxsum<<endl;
}

