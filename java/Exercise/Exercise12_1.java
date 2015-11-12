package ch12;
/*
 * Author = Eric_Chan
 * Create_Time = 2015/11/12
 */
import javax.swing.JFrame;
import javax.swing.JButton;
import java.awt.Color;
import java.awt.GridLayout;
public class Exercise12_1 extends JFrame {
	Exercise12_1()
	{

		this.setLayout(new GridLayout(100,100));
		JButton[][] jbt = new JButton[100][100];
		for(int i=0;i<100;i++)
		{
			for(int j=0;j<100;j++)
			{
				jbt[i][j] = new JButton();
				if(Math.abs(i-50)+Math.abs(j-50)<=30)
//				if(Math.pow(i-50,2)+Math.pow(j-50,2)<=500)
					jbt[i][j].setBackground(Color.blue);
				this.add(jbt[i][j]);
			}
		}

	}
	
	public static void main(String[] args)
	{
		JFrame circle = new Exercise12_1();
		circle.setTitle("chess");
		circle.setSize(1000, 1000);
		circle.setLocationRelativeTo(null);
		circle.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		circle.setVisible(true);
		
	}
}
