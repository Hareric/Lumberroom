/*
Author = Eric Chan
Create_Time = 2015/9/11
*/

/*
acm1001
ĳʯ�͹�˾�ƻ�����һ���ɶ������������͹ܵ����ùܵ�Ҫ����һ����n���;��������ÿ���;���Ҫ��һ�����͹ܵ������·��(���ϻ�)�����ܵ��������������n���� ����λ��,�����ǵ�x ���꣨�����򣩺�y ���꣨�ϱ���,Ӧ���ȷ�����ܵ�������λ��, ��ʹ���;������ܵ�֮������͹ܵ������ܺ���С��λ�á� ����n ���;���λ��,������;������ܵ�֮������͹ܵ���С�����ܺ�.
*/

import java.util.Scanner;
public class OilPipeline
{
	public static void main(String[] args)
	{
		Scanner input = new Scanner(System.in);
		
		int n = input.nextInt();//�����;���
		int count = 0;
		int local[] = new int[n];
		while(count < n)
			{
				input.nextInt();	//����ÿ���;��ĺ�����
				local[count] = input.nextInt();	//����ÿ���;���������
				count++;
			}
			
		//ʹ��ð��������;����������������
		
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
		
		//��������Ĵ�С��������Ϊ���ܵ��ĺ�����󣬼���ÿ���;������ܵ��ľ���
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