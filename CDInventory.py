#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# RBengu,     2021-Aug-13, Filled in TO-DOs
# RBengu,     2021-Aug-20, Added binary support and exception handling
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """ Processes data during runtime """
    @staticmethod
    def add_cd(strID, strTitle, stArtist):
        """
        Adds CD to data structure (list of dicts)
        
        Args:
            strID (string): ID for new entry
            
            strTitle (string): Title of CD to be added
                
            stArtist (string): Artist of CD to be added
                
        Returns:
            None. 
        """
        try:
            intID = int(strID)
            dicRow = {'ID': intID, 'Title': strTitle, 'Artist': stArtist}
            lstTbl.append(dicRow)
        
        except ValueError as e:
            print('The ID must be an integer')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep='\n')
        

        
    @staticmethod
    def del_cd(intIDDel, table):
        """
        Deletes CD from data structure (list of dicts)
        
        Args:
            intIDDel (int): ID of entry to be deleted
            
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None. 
        """
        
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """
        Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table (list of dict): 2d data structure (list of dicts) that holds the data during runtime
            
        """
        
        try:
            table.clear()
            with open(file_name, 'rb') as objFile:
                table = pickle.load(objFile)
            return table
        
        except FileNotFoundError as e:
            print('Data file does not exist!')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep='\n')
        

    @staticmethod
    def write_file(file_name, table):
        """
        Writes data from list of dictionaries to file
        
        Args:
            file_name (string): name of file to save data to
            
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None
        """
        
        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """
        Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """
        Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """
        Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        
    @staticmethod
    def new_entry():
        """
        Asks the user to enter details for their new entry, and adds it to memory
        
        Args:
            None.
        
        Returns:
            ID (string): ID of new entry
            
            Title (string): Title of new entry
            
            Artist(string): Artist of new entry
        """
        
        ID = input('Enter ID: ').strip()
        title = input('What is the CD\'s title? ').strip()
        artist = input('What is the Artist\'s name? ').strip()
        
        return ID, title, artist
        
        
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.3 process add a CD
    elif strChoice == 'a':
        
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strTitle, stArtist = IO.new_entry()
        
        # 3.3.2 Add item to the table
        DataProcessor.add_cd(strID, strTitle, stArtist)
        continue  # start loop back at top.
    
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.5 process delete a CD
    elif strChoice == 'd':
        
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        
        # 3.5.1.2 ask user which ID to remove
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        except ValueError as e:
            print('User input must be an integer')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep='\n')
            
        # 3.5.2 search thru table and delete CD
        DataProcessor.del_cd(intIDDel, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.6 process save inventory to file
    elif strChoice == 's':
        
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




