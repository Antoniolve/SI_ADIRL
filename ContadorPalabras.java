import javax.swing.*;
import javax.swing.text.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.StringTokenizer;

public class ContadorPalabras extends JFrame {
    private JTextPane textoInput;
    private JLabel resultadoPalabrasLabel;
    private JLabel resultadoConectoresLabel;

    public ContadorPalabras() {
      
        setTitle("Contador de Palabras y Conectores");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(false);

        textoInput = new JTextPane();
        JButton contarButton = new JButton("Contar");
        JButton limpiarButton = new JButton("Limpiar");
        resultadoPalabrasLabel = new JLabel("Palabras: 0");
        resultadoConectoresLabel = new JLabel("Conectores: 0");

       
        setLayout(new BoxLayout(getContentPane(), BoxLayout.Y_AXIS));
        setLocationRelativeTo(null);
        
        add(new JScrollPane(textoInput));
        add(contarButton);
        add(limpiarButton);
        add(resultadoPalabrasLabel);
        add(resultadoConectoresLabel);

        
        contarButton.addActionListener(new ActionListener() {
                        public void actionPerformed(ActionEvent e) {
                contarPalabrasYConectores();
            }
        });

       
        limpiarButton.addActionListener(new ActionListener() {
            
            public void actionPerformed(ActionEvent e) {
                limpiarPantalla();
            }
        });
    }

    private void contarPalabrasYConectores() {
        String texto = textoInput.getText();

        // Contar palabras
        StringTokenizer tokenizer = new StringTokenizer(texto, " \t\n\r\f.,;:!?'\"()[]{}<>*&^%$#@+-=|`~\\/");
        int palabras = tokenizer.countTokens();
        resultadoPalabrasLabel.setText("Palabras: " + palabras);

        
        Set<String> conectores = new HashSet<>(Arrays.asList(
                "y","de","es","una","es decir","lo","la","al","del","se", "o", "pero", "sin embargo", "además", "por lo tanto", "en conclusión",
                "por último", "finalmente", "en resumen", "en definitiva", "en fin",
                "para que", "a fin de que", "con el propósito de", "con el fin de", "con el objetivo de",
                "asimismo", "igualmente", "de igual manera", "adicionalmente", "también",
                "por otro lado", "por otra parte", "por otro parte", "así", "entonces",
                "por consiguiente", "así que", "por lo tanto", "por ende", "por eso",
                "porque", "ya que", "pues", "debido a que", "a causa de",
                "por ejemplo", "por instancia", "como", "tal como", "según",
                "comparado con", "a diferencia de", "al contrario de",
                "primero", "en primer lugar", "segundo", "en segundo lugar", "finalmente",
                "para", "al mismo tiempo", "posteriormente", "anteriormente", "luego",
                "por consiguiente", "en cambio", "de otro modo", "aunque", "si bien","el","en","un","los","las",
                "les", "que","con"
        ));

        StyledDocument doc = textoInput.getStyledDocument();
        Style estiloRojo = doc.addStyle("Rojo", null);
        StyleConstants.setForeground(estiloRojo, Color.RED);

        for (String conector : conectores) {
            
            String regex = "\\b" + conector + "\\b";
            int indice = -1;
            while ((indice = texto.toLowerCase().indexOf(conector.toLowerCase(), indice + 1)) != -1) {
                if (isPalabraCompleta(texto, indice, conector.length())) {
                    doc.setCharacterAttributes(indice, conector.length(), estiloRojo, false);
                }
            }
        }

        // Contar total de conectores encontrados
        int conectoresEncontrados = 0;
        for (String conector : conectores) {
            int indice = -1;
            while ((indice = texto.toLowerCase().indexOf(conector.toLowerCase(), indice + 1)) != -1) {
                if (isPalabraCompleta(texto, indice, conector.length())) {
                    conectoresEncontrados++;
                }
            }
        }

        resultadoConectoresLabel.setText("Conectores: " + conectoresEncontrados);
    }

    private boolean isPalabraCompleta(String texto, int indice, int longitudConector) {
        // Verificar que el conector no esté dentro de otra palabra
        if (indice > 0 && Character.isLetterOrDigit(texto.charAt(indice - 1))) {
            return false;
        }

        if (indice + longitudConector < texto.length() && Character.isLetterOrDigit(texto.charAt(indice + longitudConector))) {
            return false;
        }

        return true;
    }

    private void limpiarPantalla() {
        textoInput.setText("");
        resultadoPalabrasLabel.setText("Palabras: 0");
        resultadoConectoresLabel.setText("Conectores: 0");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new ContadorPalabras().setVisible(true);
            }
        });
    }
}