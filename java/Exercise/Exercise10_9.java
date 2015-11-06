package ch10;
/*
 * Author = Eric_Chan
 * Create_Time = 2015/10/22
 */
public class Exercise10_9 {
	public static void main(String[] args)
	{
		Course courseMath = new Course("Math");
		courseMath.addStudent("Vincent");
		courseMath.addStudent("Sponge");
		courseMath.addStudent("Eric");
		System.out.println(courseMath.toString());
		
		courseMath.dropStudent("Sponge");
		System.out.println(courseMath.toString());
		courseMath.clear();
	}
	

}

class Course
{
	private String courseName;
	private int numOfStudent = 0; //������¼��ǰѧ��������
	private int n = 20;//��ǰѧ������Ĵ�С
	private String[] students = new String[n];
	
	public Course(String courseName)
	{
		this.courseName = courseName;
	}
	
	public void addStudent(String studentName)//Ϊѧ�����������ѧ��
	{
		this.students[numOfStudent] = studentName;
		numOfStudent++;
		
		if(numOfStudent == n)//��ѧ���������� �Զ���������
		{
			n += 20;
			String[] students = new String[n];
			for(int i=0;i<numOfStudent;i++)
				students[i] = this.students[i];
			this.students = students;
		}
	}
	
	public String[] getStudents()
	{
		return this.students;
	}
	
	public int getNumOfStudent()
	{
		return this.numOfStudent;
	}
	
	public String getCourseName()
	{
		return this.courseName;
	}
	
	public void dropStudent(String student)
	{
		String[] temp_students = new String[this.n];
		int numOfStudent=this.numOfStudent;
		for(int i=0,j=0;i<this.numOfStudent;i++)
		{
			
			if (this.students[i].equals(student))
			{
				numOfStudent--;
				continue;
			}
			else
			{
				temp_students[j++] = this.students[i];
			}
				
		}
		this.students = temp_students;
		this.numOfStudent = numOfStudent;
	}
	
	public void clear()
	{
		this.students = new String[n];
		this.numOfStudent = 0;
	}
	
	public String toString()
	{
		String returnString = "";
		returnString += "��Ŀ��" + this.courseName + '\n' + "����ѧ������:" + this.numOfStudent + '\n';
		returnString += "ѧ������\n";
		for(int i=0;i<this.numOfStudent;i++)
			returnString += (this.students[i] + " ");	
		return returnString;
	}	
}
