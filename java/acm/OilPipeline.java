/*
Author = Eric Chan
Create_Time = 2015/9/11
*/

/*
acm1001
某石油公司计划建造一条由东向西的主输油管道。该管道要穿过一个有n口油井的油田。从每口油井都要有一条输油管道沿最短路经(或南或北)与主管道相连。如果给定n口油 井的位置,即它们的x 坐标（东西向）和y 坐标（南北向）,应如何确定主管道的最优位置, 即使各油井到主管道之间的输油管道长度总和最小的位置。 给定n 口油井的位置,计算各油井到主管道之间的输油管道最小长度总和.
*/

import java.util.Scanner;
public class OilPipeline
{
	public static void main(String[] args)
	{
		Scanner input = new Scanner(System.in);
		
		int n = input.nextInt();//输入油井数
		int count = 0;
		int local[] = new int[n];
		while(count < n)
			{
				input.nextInt();	//输入每个油井的横坐标
				local[count] = input.nextInt();	//输入每个油井的纵坐标
				count++;
			}
			
		//使用冒泡排序对油井的纵坐标进行排序
		
		int temp;
		for(int i=1;i<n;i++)
			for(int j=n-1;j>=i;j--)
			{
				if (local[j]>local[j-1])
					{
						temp = local[j];
						local[j] = local[j-1];
						local[j-1] = temp;
					}
			}
		
		//以纵坐标的大小的中数作为主管道的横坐标后，计算每口油井到主管道的距离
		int middle_n = n/2;
		int sum = 0;
		for(int i=0;i<n;i++)
			if(i<=middle_n)
				sum += (local[i]-local[middle_n]);
			else
				sum += (local[middle_n]-local[i]);
		
		System.out.print(sum);
				
		
	
	}
}