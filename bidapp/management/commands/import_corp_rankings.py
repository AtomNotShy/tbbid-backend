from django.core.management.base import BaseCommand
from bidapp.models import CorpList
import psycopg2
from psycopg2.extras import DictCursor

class Command(BaseCommand):
    help = 'Import company rankings from PostgreSQL database'

    def handle(self, *args, **options):
        # Database connection parameters
        db_params = {
            'host': 'localhost',
            'port': 5432,
            'dbname': 'xizang',
            'user': 'atom',
            'passwd': ''
        }

        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(
                host=db_params['host'],
                port=db_params['port'],
                dbname=db_params['dbname'],
                user=db_params['user'],
                password=db_params['passwd']
            )
            
            # Create a cursor
            with conn.cursor(cursor_factory=DictCursor) as cur:
                # Query to get company rankings
                cur.execute("""
                    SELECT 
                        name,
                        bid_count,
                        bid_success_count
                    FROM corp_list
                    ORDER BY bid_success_count DESC
                """)
                
                # Fetch all results
                results = cur.fetchall()
                
                # Process each result
                for row in results:
                    # Update or create CorpList entry
                    corp, created = CorpList.objects.update_or_create(
                        company_name=row['name'],
                        defaults={
                            'bid_count': row['bid_count'],
                            'bid_count_success': row['bid_success_count']
                        }
                    )
                    
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created new entry for {row["name"]}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Updated entry for {row["name"]}'))
                
                self.stdout.write(self.style.SUCCESS('Successfully imported company rankings'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))
        finally:
            if 'conn' in locals():
                conn.close() 