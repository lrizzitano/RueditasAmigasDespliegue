          /*
          # We define the required patterns as Regex
          # 1. LoadBalancer -> Server pattern
          # 2. Server -> Database pattern
          # 3. Internet/Cloud to LoadBalancer
          
          DIAGRAM_FILE="diagrams/" # Change to your actual path
          
          echo "Validating architectural patterns..."
          
          # Check for Load Balancer connection
          grep -qP '"LoadBalancer" --> "Servidor1RueditasAmigas" : HTTP' $DIAGRAM_FILE || { echo "❌ Missing LoadBalancer pattern"; exit 1; }
          
          # Check for Database connection
          grep -qP 'Servidor.*-->.*BaseDeDatos' $DIAGRAM_FILE || { echo "❌ Missing Database connection pattern"; exit 1; }
          
          # Check for Internet/Cloud and HTTPS
          grep -qE 'cloud|Internet' $DIAGRAM_FILE || { echo "❌ Missing Internet/Cloud component"; exit 1; }
          grep -q "HTTPS" $DIAGRAM_FILE || { echo "❌ Missing HTTPS definition"; exit 1; }
          
          echo "✅ Architecture structure matches requirements."
          */