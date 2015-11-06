/*
 * Author = Eric_Chan
 * Create_Time = 2015/11/4
 */
import java.util.Date;
public class Exercise11_8
{
	public static void main(String[] args)
	{
		Account user_1 = new Account(1122,1000,"George");
		user_1.setAnnualInterstRate(0.015);
		user_1.deposit(30, "��һ�δ�Ǯ");
		user_1.deposit(40, "�ڶ��δ�Ǯ");
		user_1.deposit(50, "�����δ�Ǯ");
		user_1.withDraw(5, "��һ��ȡǮ");
		user_1.withDraw(4, "�ڶ���ȡǮ");
		user_1.withDraw(2, "������ȡǮ");
		System.out.println(user_1.toString());
	}
}



class Account
{
	private int id = 0;
	private double balance = 0;
	private double annualInterestRate = 0; //��ʾ��ǰ����
	private Date dataCreated = new Date();
	private String name; //��¼�˻��û���
	private java.util.ArrayList transactions = new java.util.ArrayList(); //��¼���˻����׵��б�
	
	class Transaction //��ϸ��¼ÿһ�ʽ��׵���
	{
		private char type;//��¼���׵����� 'W'��ʾȡǮ ; 'D'��ʾ��Ǯ
		private Date date = new Date();//������¼���׵�ʱ��
		private double amount;//��¼���׵�����
		private double balance;//ʣ��Ľ��
		private String description ;//��¼���׵�����
		
		Transaction(char type,double amount,double balance,String description)
		{
			this.type = type;
			this.amount = amount;
			this.balance = balance;
			this.description = description;
		}
		
		public String toString()
		{
			return type + "   |" + date.toString() + "| " + amount +" |   " + balance +"   |" +  description + '\n'; 
		}
	}
	
	
	Account(){		
	}
	
	Account(int id,double balance)
	{
		this.id = id;
		this.balance = balance;
	}
	
	Account(int id,double balance,String name)
	{
		this(id,balance);
		this.name = name;
	}
	
	void setID(int id)
	{
		this.id = id;
	}
	
	int getID()
	{
		return this.id;
	}
	
	void setBalance(double balance)
	{
		this.balance = balance;
	}
	
	double getBalance()
	{
		return this.balance;
	}
	
	void setAnnualInterstRate(double annualInterstRate)
	{
		this.annualInterestRate = annualInterstRate;
	}
	
	double getAnnualInterstRate()
	{
		return this.annualInterestRate;
	}
	
	String getDateCreated() //���ش��������ʱ��
	{
		return this.dataCreated.toString();
	}
	
	double getMonthlyInterestRate()//����������
	{
		return this.annualInterestRate / 12 ;
	}
	
	void withDraw(double lessMoney,String description)//ȡǮ
	{
		this.balance -= lessMoney;
		Transaction my_transaction = new Transaction('W' , lessMoney , this.balance ,description);
		this.transactions.add(my_transaction);
	}
	
	void deposit(double addMoney,String description)//��Ǯ
	{
		this.balance += addMoney;
		Transaction my_transaction = new Transaction('D' , addMoney , this.balance ,description);
		this.transactions.add(my_transaction);
	}
	
	public String toString()
	{
		return  "����:" + this.name + " ����:" + this.annualInterestRate + " ��֧��:" + this.balance + '\n'
				+ "�������� |             ����ʱ��                     |���׵�����|  ���         | ����\n"
				+ this.transactions.toString();
	}
	
	
}
