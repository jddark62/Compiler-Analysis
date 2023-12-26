#define forloop	for(i=0;i<n;i++)\
			{\
				for(j=0;j<n;j++)\
				    {\
				        printf("%d",a[i][j]);\
				    }\
			}
main()
{
		int i,j,n=2,a[10][10];
		for(i=0;i<n;i++)
		 {
		     for(j=0;j<n;j++)
		     {
		         scanf(“%d”,&a[i][j]);
		    }
		}
		forloop
}
